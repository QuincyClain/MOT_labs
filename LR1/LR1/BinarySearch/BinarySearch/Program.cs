using System;

class Program
{
    static int BinarySearch(int[] array, int searchedValue, int first, int last)
    {
        if (first > last)
        {
            return -1;
        }

        var middle = (first + last) / 2;
        var middleValue = array[middle];

        if (middleValue == searchedValue)
        {
            return middle;
        }
        else
        {
            if (middleValue > searchedValue)
            {
                return BinarySearch(array, searchedValue, first, middle - 1);
            }
            else
            {
                return BinarySearch(array, searchedValue, middle + 1, last);
            }
        }
    }
    static void Main(string[] args)
    {
        Console.Write("Введите элементы массива: ");
        var s = Console.ReadLine().Split(new[] { " ", ",", ";" }, StringSplitOptions.RemoveEmptyEntries);
        var array = new int[s.Length];
        for (int i = 0; i < s.Length; i++)
        {
            array[i] = Convert.ToInt32(s[i]);
        }

        Array.Sort(array);
        Console.WriteLine("Упорядоченный массив: {0}", string.Join(", ", array));

        while (true)
        {
            Console.Write("Введите искомое значение");
            var k = Convert.ToInt32(Console.ReadLine());
            if (k == -1)
            {
                break;
            }

            var searchResult = BinarySearch(array, k, 0, array.Length - 1);
            if (searchResult < 0)
            {
                Console.WriteLine("Элемент со значением {0} не найден", k);
            }
            else
            {
                Console.WriteLine("Элемент найден. Индекс элемента со значением {0} равен {1}", k, searchResult);
            }
        }

        Console.ReadLine();
    }
}