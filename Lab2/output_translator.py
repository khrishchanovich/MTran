if __name__ == "__main__":
	arr = [64, 25, 12, 22, 11]
	n = len(arr)
	for i in range(n -1):
		for j in range(n -i -1):
			if arr[j]>arr[j +1]:
				temp = arr[j]
				arr[j] = arr[j +1]
				arr[j +1] = temp



	print("Sorted array: ")
	for i in range(n):
		print(arr[i])

	print()
	
