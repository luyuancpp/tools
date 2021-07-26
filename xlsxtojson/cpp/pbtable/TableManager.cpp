#include "TableManager.h"

#include "json.pb.h"

TableManager gTableManager;

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
	reload_callback_.push_back(std::move(cb));
}

