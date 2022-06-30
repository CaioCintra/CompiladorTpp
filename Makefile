all:
	clang -emit-llvm -S io.c
	llc -march=x86-64 -filetype=obj io.ll -o io.o
	python3 tppgenerator.py geracao-codigo-testes/gencode-004.tpp
	llvm-link modulo.ll io.ll -o modulo.bc
	clang modulo.bc -o modulo.o

clean:
	rm *.ll *.o *.bc