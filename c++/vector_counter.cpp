#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

class Counter {
    private:
    int count = 0;
    char choice;
    char start_over;
    std::vector<int> vector_count;

    int IncludeSaveData()
    {
        std::fstream sc{"saved_count.txt"};
        std::string string_count;
        while (sc)
        {
            std::getline(sc, string_count);
        }
        count = std::stoi(string_count);

        return count;
    }

    void SaveData(int count)
    {
        std::fstream sd{"saved_count.txt", std::ios::out};
        sd << count;

        std::cout << "Count saved in saved_count.txt\n";
    }

    void AddToVector(int count)
    {
        vector_count.push_back(count);
        std::cout << "Added " << count << " to vector!\n";
    }

    void SortVector()
    {
        std::sort(vector_count.begin(), vector_count.end());
    }
    
    int RunCounter(int count)
    {   
        choice = 'Y';
        while (choice != 'N')
        {
            count += 1;
            std::cout << count << '\n' <<"Keep counting? Y/N\n";
            std::cin >> choice;
        }

        if (choice == 'N')
        {
            std::cout << "Start over? Y/N\n";
            std::cin >> start_over;
            AddToVector(count);

            if (start_over == 'Y')
            {
                StartCount(start_over);
            }
            else
            {
                std::cout << "Save count? Y/N\n";
                std::cin >> choice;

                if (choice == 'Y')
                {
                    SaveData(count);
                }
            }
        }
        return count;
    }

    public:
    void StartCount(char start_over = 'N')
    {
        if (start_over == 'N')
        {
            std::fstream saved{"saved_count.txt"};
            if (saved.good())
            {
                std::cout << "Keep saved data?: Y/N\n";
                std::cin >> choice;

                if (choice == 'Y')
                {
                    std::string saved_count;
                    while (saved)
                    {
                        std::getline(saved, saved_count);
                    }
                    int count = std::stoi(saved_count);
            
                    RunCounter(count);
                }
                else
                {
                    RunCounter(count);
                }
            }
            else
            {
                RunCounter(count);
            }
            
        }
        else
        {
            RunCounter(count = 0);
        }
        
    }

    Counter()
    {
        std::cout << "Initiated count..\n";
    }

    ~Counter()
    {
        std::cout << "Destructed!";
    }
    
    void SearchVector(std::vector<int> search) //Solely created to test search
    {
        std::vector<int>::iterator i;
        i = std::search(vector_count.begin(), vector_count.end(), search.begin(), search.end());
        std::cout << "Found at index: " << (i - vector_count.begin()) << "\n";
    }
    void PrintVector()
    {
        std::cout << "[";
        for (int i = 0; i < vector_count.size() - 1; i++)
        {
            std::cout << vector_count[i] << ",";
        }
        std::cout << vector_count[vector_count.size()-1] << "]\n";
    }

};

int main()
{   
    Counter c;
    c.StartCount();
    //std::vector<int> test{1,2};
    c.PrintVector();
};