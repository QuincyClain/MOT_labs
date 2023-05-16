using System;

public class Program {
    public static void Main() {
        Console.WriteLine("Before sorting:");
        Console.WriteLine(string.Join(", ", arr));

        Sort(arr);

        Console.WriteLine("After sorting:");
        Console.WriteLine(string.Join(", ", arr));
    }

    public static void Sort(int[] arr) {
        int n = arr.Length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}