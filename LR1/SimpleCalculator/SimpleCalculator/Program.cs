using System;
    class Program
    {
        static void Main(string[] args)
        {
            string cont;

            do
            {
                double first;
                double second;
                string operation;
                double answer;

                Console.Clear();
                Console.WriteLine("Первое число: ");
                first = Convert.ToDouble(Console.ReadLine());

                Console.WriteLine("Действие %, *, /, +, - : ");
                operation = Convert.ToString(Console.ReadLine());

                Console.WriteLine("Второе число: ");
                second = Convert.ToDouble(Console.ReadLine());

                if (operation == "+")
                {
                    answer = first + second;
                    Console.WriteLine("Результат: " + answer);
                }

                if (operation == "-")
                {
                    answer = first - second;
                    Console.WriteLine("Результат: " + answer);
                }

                if (operation == "*")
                {
                    answer = first * second;
                    Console.WriteLine("Результат: " + answer);
                }

                if (operation == "/")
                {
                    answer = first / second;
                    Console.WriteLine("Результат: " + answer);
                }

                if (operation == "%")
                {
                    answer = first % second;
                    Console.WriteLine("Результат: " + answer);
                }

                Console.WriteLine("Совершить еще одну операцию?");
                cont = Convert.ToString(Console.ReadLine());

            } while (cont == "yes");

        }
    }