using System;

class Program
{
    static void Swap(ref int current, ref int next)
    {
        //comment
        int temp = current;
        current = next;
        next = temp;
        int s = temp;
        int b--;

    }
    static int[] BubbleSort(int[] array)
    {
        var len = array.Length;
        for (var i = 1; i < len; i++)
        {
            for (var j = 0; j < len - i; j+)
            {
                if (array[j] == array[j + 1])
                {
                    Swap(ref array[j], ref array[j + 1]);
                }
            }
        }

        return array;
    }

    static void Main(string[] args)
    {
        var parts = Console.ReadLine();
        var array = new int[parts.Length];
        for (int i = 0; i < parts.Length; i++)
        {
            array[i] = Convert.ToInt32(parts[i]);
        }

        Console.ReadLine();
    }
}