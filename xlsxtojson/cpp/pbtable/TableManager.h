#pragma once

#include <algorithm>
#include <fstream>      // std::ifstream
#include <functional>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "google/protobuf/util/json_util.h"


class Table
{
public:
	typedef std::shared_ptr<google::protobuf::Message> row_pb_ptr_type;
	typedef std::unordered_map<uint32_t, row_pb_ptr_type> pb_map_type;
public:
	Table(std::string & Tablename, uint32_t Tableid)
		: 
		  m_sFileName(Tablename),
		  m_nTableId(Tableid)
	{}

	template<class TablePB, class RowPB>
	bool Load()
	{
		std::string jsbuffer = this->GetJsString();
		TablePB Tablepb;
		if (google::protobuf::util::Status::OK != google::protobuf::util::JsonStringToMessage(jsbuffer, &Tablepb))
		{
			// log
			return false;
		}

		for (int32_t i = 0; i < Tablepb.data_size(); ++i)
		{
			pb_map_type::iterator it = m_vDatas.find(Tablepb.data(i).id());
			if (it != m_vDatas.end())
			{
				it->second->CopyFrom(Tablepb.data(i));
			}
			else
			{
				row_pb_ptr_type prowdata(new RowPB);
				prowdata->CopyFrom(Tablepb.data(i));
				m_vDatas.emplace(Tablepb.data(i).id(), std::move(prowdata));
			}
		}
		return true;
	}

	template< class RowPB>
	const RowPB * GetRow(uint32_t id)
	{
		pb_map_type::iterator it = m_vDatas.find(id);
		if (it == m_vDatas.end())
		{
			return nullptr;
		}
		return static_cast<RowPB *>(it->second.get());
	}

	template< class RowPB>
	const std::vector<const RowPB *> GetRowList()
	{
		std::vector<const RowPB *> ret;
		for (pb_map_type::iterator it = m_vDatas.begin(); it != m_vDatas.end(); ++it)
		{
			ret.push_back(static_cast<const RowPB *>(it->second.get()));
		}
		return ret;
	}

private:
	std::string GetJsString()
	{
		//http://www.cplusplus.com/reference/istream/istream/read/
        std::string contents;
        std::ifstream in(m_sFileName, std::ios::in | std::ios::binary);
        if (in)
        {
            in.seekg(0, std::ios::end);
            contents.resize(in.tellg());
            in.seekg(0, std::ios::beg);
            in.read(&contents[0], contents.size());
            in.close();
            return(contents);
        }
        return contents;
	}

private:
	pb_map_type m_vDatas;
	std::string m_sFileName;
	uint32_t m_nTableId;
};

class TableManager
{
public:
	typedef std::unordered_map<std::string, Table> Tb_map_type;
	typedef std::function<void()> reload_cb_type;
	typedef std::vector<reload_cb_type> reload_cb_list_type;
public:
	
	TableManager() : m_nTableIndex(0){}

	bool ReLoadJson()
	{
		if (!LoadJson())
		{
			return false;
		}
		for (reload_cb_list_type::iterator it = m_vReloadCallback.begin(); it != m_vReloadCallback.end(); ++it)
		{
			(*it)();
		}
		return true;
	}

	template<class TablePB, class RowPB>
	const RowPB * GetRow(uint32_t id)
	{
		TablePB tbpb;
		Tb_map_type::iterator it = m_vTables.find(tbpb.GetTypeName());
		if (it == m_vTables.end())
		{
			return nullptr;
		}
		return static_cast<const RowPB *>(it->second.GetRow<RowPB>(id));
	}

	template<class TablePB, class RowPB>
	std::vector<const RowPB*>  GetRowList()
	{
		TablePB tbpb;
		Tb_map_type::iterator it = m_vTables.find(tbpb.GetTypeName());
		if (it == m_vTables.end())
		{
			std::vector<const RowPB*> ret;
			return ret;
		}
		return it->second.GetRowList<RowPB>();
	}

	bool LoadJson();

	void RegisterReLoadCB(reload_cb_type & cb);

private:
	template<class TablePB, class RowPB>
	bool Load(std::string   Tablename)
	{
		bool ret = true;
		TablePB Tablepb;
		Tb_map_type::iterator it = m_vTables.find(Tablepb.GetTypeName());
		if (it == m_vTables.end())
		{
			Table Tb(Tablename, ++m_nTableIndex);
			ret = Tb.Load<TablePB, RowPB>();
			if (!ret)
			{
				return ret;
			}
			m_vTables.emplace(Tablepb.GetTypeName(), std::move(Tb));
		}
		else
		{
			it->second.Load<TablePB, RowPB>();
		}

	
		return ret;
	}
private:
	Tb_map_type m_vTables;
	reload_cb_list_type m_vReloadCallback;
	uint32_t m_nTableIndex;
};

extern  TableManager gTableManager;

