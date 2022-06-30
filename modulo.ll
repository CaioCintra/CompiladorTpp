; ModuleID = "modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare void @"escrevaInteiro"(i32 %".1") 

declare i32 @"leiaInteiro"() 

declare void @"escrevaFlutuante"(float %".1") 

declare float @"leiaFlutuante"() 

@"n" = global i32 0, align 4
@"soma" = global i32 0, align 4
define i32 @"main"() 
{
entry:
  store i32 10, i32* @"n"
  store i32 0, i32* @"soma"
  br label %"loop"
exit:
  %".12" = load i32, i32* @"soma"
  call void @"escrevaInteiro"(i32 %".12")
  %"retorno" = alloca i32, align 4
  ret i32 0
validate:
  %"a_cmp" = load i32, i32* @"n", align 4
  %"if_test_1" = icmp eq i32 %"a_cmp", 0
  br i1 %"if_test_1", label %"exit", label %"loop"
loop:
  %".5" = load i32, i32* @"soma"
  %".6" = load i32, i32* @"n"
  %"add" = add i32 %".5", %".6"
  store i32 %"add", i32* @"soma"
  %".8" = load i32, i32* @"n"
  %"sub" = sub i32 %".8", 1
  store i32 %"sub", i32* @"n"
  br label %"validate"
}
