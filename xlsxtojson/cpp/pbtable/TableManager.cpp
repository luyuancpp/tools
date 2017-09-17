#include "TableManager.h"

#include "json.pb.h"

TableManager g_oTableManager;

static std::string jsdir("./Server/Tableig/Json");


bool TableManager::LoadJson()
{

	if (!Load<GtestTable, GtestTableRow>("../json/gtest.json"))
	{
		return false;
	}

	return true;
}

void TableManager::RegisterReLoadCB(reload_cb_type & cb)
{
	m_vReloadCallback.push_back(std::move(cb));
}

