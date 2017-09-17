#include "Remind.h"

#include <stdio.h>

namespace RemindModel
{


//
void Remind::Copy(const Remind & tRemind)
{
    printf("Remind::Copy\n");
}


void Remind::OnKickUp(ObjPlayer * tpObjPlayer)
{
    printf("Remind::OnKickUp");
    TestPrivateFunction();
}

void Remind::TestPrivateFunction()
{
    printf("Remind::TestPrivateFunction\n");
}

} // namespace RemindModel


