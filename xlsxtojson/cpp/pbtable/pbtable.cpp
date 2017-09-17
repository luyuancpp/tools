#include <iostream>

#include <gtest/gtest.h>


#include "TableManager.h"
#include "json.pb.h"



using namespace std;


TEST(JsonTableTest, LoadJson)
{
	EXPECT_TRUE(g_oTableManager.LoadJson());

	const GtestTableRow * pData = g_oTableManager.GetRow<GtestTable, GtestTableRow>(1);
	if (pData != NULL)
	{
	cout << "id :" << pData->id() << endl;
	for (int32_t i = 0; i < pData->thread_id_size(); ++i)
	{
	cout << pData->thread_id(i) << ",";
	}

	cout << endl;

	cout << "name :" << pData->name() << endl;
	}
}

TEST(JsonTableTest, ReLoadJson)
{
	EXPECT_TRUE(g_oTableManager.ReLoadJson());

	const GtestTableRow * pData = g_oTableManager.GetRow<GtestTable, GtestTableRow>(1);
	if (pData != NULL)
	{
		cout << "id :" << pData->id() << endl;
		for (int32_t i = 0; i < pData->thread_id_size(); ++i)
		{
			cout << pData->thread_id(i) << ",";
		}

		cout << endl;

		cout << "name :" << pData->name() << endl;
	}
}

TEST(JsonTableTest, ListTable)
{
	EXPECT_TRUE(g_oTableManager.ReLoadJson());

	std::vector<const GtestTableRow *> pData = g_oTableManager.GetRowList<GtestTable, GtestTableRow>();

	for (std::vector<const GtestTableRow *>::iterator it = pData.begin(); it != pData.end(); ++it)
	{
	cout << "id :" << (*it)->id() << endl;
	for (int32_t i = 0; i < (*it)->thread_id_size(); ++i)
	{
	cout << (*it)->thread_id(i) << ",";
	}

	cout << endl;
	cout << "name :" << (*it)->name() << endl;
	}
}


TEST(JsonTableTest, GetTableName)
{
	GtestTableRow Tablerow;
	GtestTable Table;
	cout << "name :" << Tablerow.GetTypeName() << endl;
	cout << "name :" << Table.GetTypeName() << endl;

	EXPECT_EQ("GtestTableRow", Tablerow.GetTypeName());
	EXPECT_EQ("GtestTable", Table.GetTypeName());
}

int main(int argc, char **argv)
{

	testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}


