#include <assert.h>
#include <iostream>
#include <memory>

#include "../genfile/Costomdes.h"
#include "../genfile/CostomdesDerived.h"
#include "../genfile/DBStream.h"
#include "../genfile/gametype.h"
#include "../genfile/MailBox.h"
#include "../genfile/Remind.h"
#include "../genfile/RemindBoxManager.h"
#include "../genfile/StdTest.h"
#include "../genfile/TestDefineLen.h"
#include "../genfile/TemplateTest.h"


using namespace std;

int main(void)
{
	shared_ptr<DBStream> p(new DBStream);
    p->SetMaxCharLen(1);
    assert(!p->Write(NULL, 0));
    assert(!p->Read(NULL, 0));
    cout << p->GetMaxCharLen() <<endl;

    RemindModel::RemindTimer tTimer;
    tTimer.SetYear(1992);
    assert(tTimer.GetYear() == 1992);

    shared_ptr<RemindModel::Remind> pr(new RemindModel::Remind);
    char ph[] = "hello";
    pr->SetFirstStr(ph);
    cout << pr->GetFirstStr() << endl;
    pr->SetTimer(tTimer);
    assert(pr->GetTimer().GetYear() == 1992);
    assert(pr->GetTimer().GetMonth() == 0);
    

    shared_ptr<RemindModel::Mail> pm(new RemindModel::Mail);
    RemindModel::Remind * pRemind = pm.get();
    pRemind->Copy(*pm.get());
    pRemind->OnKickUp(NULL);

    shared_ptr<RemindModel::MailBox> pmb(new RemindModel::MailBox);
    RemindModel::Mail tMail;
    pmb->AddMail(tMail);

    shared_ptr<RemindModel::RemindBoxManager> prm(new RemindModel::RemindBoxManager);

    int tArr[TestDefineLen::TEST_LEN] = {1};
    TestDefineLen tTestLen;
    tTestLen.SetCollection(tArr);
    for (int i = 0 ; i < 2; ++i)
    {
        cout << tTestLen.GetCollection()[i] << endl;
    }

    shared_ptr<Costomdes> pc(new CostomdesDerived);

    TemplateTest<int> test;


	return 0;
}
