; ModuleID = "modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = global i32 0, align 4
define i32 @"main"() 
{
entry:
  %"ret" = alloca i32, align 4
  store i32 0, i32* %"ret"
  %"cmp1" = load i32, i32* %"ret", align 4
  %"cmp2" = load i32, i32* %"ret", align 4
  %"if_test_1" = icmp slt i32 %"cmp1", %"cmp2"
  br i1 %"if_test_1", label %"iftrue_1", label %"iffalse_1"
exit:
  %"retorno" = alloca i32, align 4
  %".12" = load i32, i32* %"ret"
  ret i32 %".12"
iftrue_1:
  store i32 5, i32* %"ret"
  br label %"ifend_1"
iffalse_1:
  store i32 6, i32* %"ret"
  br label %"ifend_1"
ifend_1:
  store i32 10, i32* @"a"
  store i32 1, i32* %"ret"
  store i32 0, i32* %"ret"
  br label %"exit"
}
