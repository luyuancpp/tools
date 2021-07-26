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
	Table(std::string & file_name, uint32_t table_id)
		: 
		  file_name_(file_name),
		  table_id_(table_id)
	{}

	template<class TablePB, class RowPB>
	bool Load()
	{
		std::string jsbuffer = this->GetJsString();
		TablePB tpb;
		if (google::protobuf::util::Status::OK != google::protobuf::util::JsonStringToMessage(jsbuffer, &tpb))
		{
			// log
			return false;
		}

		for (int32_t i = 0; i < tpb.data_size(); ++i)
		{
			pb_map_type::iterator it = datas_.find(tpb.data(i).id());
			if (it != datas_.end())
			{
				it->second->CopyFrom(tpb.data(i));
			}
			else
			{
				row_pb_ptr_type prowdata(new RowPB);
				prowdata->CopyFrom(tpb.data(i));
				datas_.emplace(tpb.data(i).id(), std::move(prowdata));
			}
		}
		return true;
	}

	template< class RowPB>
	const RowPB * GetRow(uint32_t id)
	{
		pb_map_type::iterator it = datas_.find(id);
		if (it == datas_.end())
		{
			return nullptr;
		}
		return static_cast<RowPB *>(it->second.get());
	}

	template< class RowPB>
	const std::vector<const RowPB *> GetRowList()
	{
		std::vector<const RowPB *> ret;
		for (pb_map_type::iterator it = datas_.begin(); it != datas_.end(); ++it)
		{
			ret.push_back(static_cast<const RowPB *>(it->second.get()));
		}
		return ret;
	}

private:
	std::string GetJsString()
	{
		//http://www.cplusplus.com/reference/istream/istream/read/
		std::ifstream is(file_name_, std::ifstream::binary);
		std::string jssbuffer;
		if (is) {
			// get length of file:
			is.seekg(0, is.end);
			int length = (int)is.tellg();
			length = length + 1;
			is.seekg(0, is.beg);
			char * buffer = new char[length];
			memset(buffer, 0, length);
			// read data as a block:
			is.read(buffer, length);
			is.close();
			// ...buffer contains the entire file...
			jssbuffer = buffer;
			jssbuffer.erase(remove_if(jssbuffer.begin(), jssbuffer.end(), iscntrl), jssbuffer.end());
			jssbuffer.erase(remove_if(jssbuffer.begin(), jssbuffer.end(), isspace), jssbuffer.end());
			delete[] buffer;	
		}
		return jssbuffer;
	}

private:
	pb_map_type datas_;
	std::string file_name_;
	uint32_t table_id_;
};

class TableManager
{
public:
	typedef std::unordered_map<std::string, Table> Tb_map_type;
	typedef std::function<void()> reload_cb_type;
	typedef std::vector<reload_cb_type> reload_cb_list_type;
public:
	
	TableManager() : table_index_(0){}

	bool ReLoadJson()
	{
		if (!LoadJson())
		{
			return false;
		}
		for (reload_cb_list_type::iterator it = reload_callback_.begin(); it != reload_callback_.end(); ++it)
		{
			(*it)();
		}
		return true;
	}

	template<class TablePB, class RowPB>
	const RowPB * GetRow(uint32_t id)
	{
		TablePB tbpb;
		Tb_map_type::iterator it = tables.find(tbpb.GetTypeName());
		if (it == tables.end())
		{
			return nullptr;
		}
		return static_cast<const RowPB *>(it->second.GetRow<RowPB>(id));
	}

	template<class TablePB, class RowPB>
	std::vector<const RowPB*>  GetRowList()
	{
		TablePB tbpb;
		Tb_map_type::iterator it = tables.find(tbpb.GetTypeName());
		if (it == tables.end())
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
		Tb_map_type::iterator it = tables.find(Tablepb.GetTypeName());
		if (it == tables.end())
		{
			Table Tb(Tablename, ++table_index_);
			ret = Tb.Load<TablePB, RowPB>();
			if (!ret)
			{
				return ret;
			}
			tables.emplace(Tablepb.GetTypeName(), std::move(Tb));
		}
		else
		{
			it->second.Load<TablePB, RowPB>();
		}

	
		return ret;
	}
private:
	Tb_map_type tables;
	reload_cb_list_type reload_callback_;
	uint32_t table_index_;
};

extern  TableManager gTableManager;

