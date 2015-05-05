installTo = $(PWD)

default:
	python setup.py build_ext --inplace
opt:
	python setup-opt.py build_ext --inplace
user:
	echo "$(installTo)/" > config/$(USER).config
	echo "$(installTo)/testing/3D/" >> config/$(USER).config
	tail -n +3 config/default.config >> config/$(USER).config
cython-test:
	cython -a readCheartData.pyx
cython-test-opt:
	cython -X boundscheck=False -X wraparound=False -X cdivision=False -a readCheartData.pyx
clean:
	rm *.so
distclean:
	rm -r build/
