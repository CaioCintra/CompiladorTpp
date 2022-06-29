; ModuleID = "modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"n" = global i32 0, align 4
@"soma" = global i32 0, align 4
define i32 @"main"() 
{
entry:
  %"retorno" = alloca i32, align 4
  store i32 0, i32* %"retorno"
  br label %"exit"
exit:
  %"ret_temp" = load i32, i32* %"retorno", align 4
  ret i32 %"ret_temp"
}
