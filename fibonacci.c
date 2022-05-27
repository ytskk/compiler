Int fibonacci(Int n) {
	if (n == 0) {
		return 0;
	}
	if (n == 1) {
		return 1;
	}

	return fibonacci(n - 1) + fibonacci(n - 2);

}

void main() {
	Int number = 1;

	print(fibonacci(number));
}





