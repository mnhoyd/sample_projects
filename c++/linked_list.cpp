#include <iostream>  // for cout
#include <vector> 

using namespace std;


/* Prosjekt hvor vi skulle lage en dobbelt-lenket liste*/

struct Node{
    int value;
    Node *next = nullptr;
    Node *prev = nullptr;
    Node(int value) : value(value){}
};

class LinkedList{
    
    Node *head = nullptr;
    Node *tail = nullptr;
    int m_size = 0;

    public:
    
        LinkedList(){}
        int length(){
            return m_size;
        }

        void append(int x){
            m_size++;
            Node *x_node = new Node(x);
            x_node->prev = tail;
            x_node->next = nullptr;
            if (tail==nullptr) {
                head = x_node;
            } else {
                tail->next = x_node;
            }
            tail = x_node;
        }

        void print(){
            cout << "[";
            Node *current = head;
            while (current->next != nullptr) {
                cout << current->value << ", ";
                current = current->next;
            }
            cout << current->value << "]\n";
        }

        ~LinkedList(){
            Node *current = head;
            Node *next_in_line = head;
            while (current != nullptr) {
                next_in_line = current->next;
                delete[] current;
                current = next_in_line;
            }
            cout << "LinkedList deleted" << endl;
        }

        int& operator[](int indx) {
            int current_indx = 0;
            Node *current = head;
            while (current != nullptr) {
                if (current_indx == indx) {
                    return current->value;
                }
                current = current->next;
                current_indx++;
            }
            throw out_of_range("Indeks " + to_string(indx) + " for stor!");
        }

        void insert(int val, int indx){
            Node *new_val = new Node(val);
            Node *current = head;
            int current_indx = 0;
            if (m_size == 0){
                append(val);
            } else if (indx == 0) {
                new_val->next = head;
                current->prev = new_val;
                head = new_val;
                m_size++;
            } else if (indx > m_size) {
                    throw out_of_range("Indeks " + to_string(indx) + " er utenfor rekkevidde");
            } else {
                while (current_indx < indx){
                current = current->next;
                current_indx++;
                }
                if (current == nullptr and m_size != 0) {
                
                append(val);

                }  else {
                    current->prev->next = new_val;
                    new_val->prev = current->prev;
                    new_val->next = current;
                    current->prev = new_val;
                    m_size++;
                }
            }

        }

        void remove(int indx){
            Node *current = head;
            int current_indx = 0;
            while (current_indx < indx){
                current = current->next;
                current_indx++;
            }
            if (indx==0) {
                current->next->prev = nullptr;
                head = current->next;
            

            } else if (current_indx == m_size-1) {
                current->prev->next = nullptr;
                tail = current->prev;
            }
            else {
            current->prev->next = current->next;
            current->next->prev = current->prev;
            }
            m_size--;
            
            delete[] current;
        }

        int pop(int indx){
            Node *current = head;
            int current_indx = 0;
            while (current_indx < indx){
                current = current->next;
                current_indx++;
            }
            int r_value = current->value;
            remove(indx);
            return r_value;
        }

        int pop(){
            Node *current = head;
            int current_indx = 0;
            while (current->next != nullptr){
                current = current->next;
                current_indx++;
            }
            int r_value = current->value;
            remove(current_indx);
            return r_value;
        }
        LinkedList(vector<int> liste){
            for (int i = 0; i < liste.size(); i++){
                append(liste[i]);
            }
        }
};