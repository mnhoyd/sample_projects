#include <iostream>  
#include <vector>  

using namespace std;

/* De initielle verdiene for ArrayList er basert på de i Lecture 14. Metodene resize, konstruktøren, destruktøren, append, print og int& operator[] er også hentet fra Lecture 14,
med noen modifikasjoner for å kunne fungere slik som vi ville */

class ArrayList {
    /* Klasse for å lage en array, 
    initielle private verdier*/
    private:
     int *m_data;
     int m_capacity = 1;
     int m_growthfact = 2;
     int m_size = 0;
    
    /* Metode for å forstørre arrayen dersom man legger til verdier og kapasiteten ikke er stor nok*/ 
     void resize(){
         int capacity = m_growthfact*m_capacity;
         int *data = new int[capacity];
         /*Løper gjennom arrayen og kopierer den til en ny*/
         for (int i = 0; i < m_size; i++) {
             data[i] = m_data[i];
         }
        
        /* Sletter den gamle arrayen og gjør om den nye til m_data */
         delete[] m_data;
         m_data = data;
         m_capacity = capacity;
     }

    /* Offentlige metoder */
    public:
     ArrayList(){
         m_data = new int[m_capacity];
     }
     
     ArrayList(vector<int> data){
         m_data = new int[m_capacity];
         for (int i=0; i < data.size(); i++){
             append(data[i]);
         }
     }

     int capacity(){
         return m_capacity;
     }

     int length(){
         return m_size;
     }
     ~ArrayList(){
         delete[] m_data;
     }

     void append(int val){
         if (m_size >= m_capacity) {
            resize();
         }
         
         m_data[m_size] = val;
         m_size++;
     }
     
     void print(){
         cout << "[";
         for (int i=0; i<m_size-1; i++) {
             cout << m_data[i] << ", ";
         }
         cout << m_data[m_size-1] << "]" << endl;
     }

     int& operator[](int indx){
         if ((indx >= m_size) || (indx < 0)) {
             throw out_of_range("Indeks " + to_string(indx) + " uttafor!");
         } 
         else {
            return m_data[indx];
         }
     }
     void insert(int val, int indx){
         if (indx > m_size){
             throw out_of_range("Indek " + to_string(indx) + " uttafor.. igjen.");
         }
         
         if (indx == m_size){
             append(val);
             return;
         }
        
         for (int i = m_size; i > indx; i--){
            m_data[i] = m_data[i-1];
         }
         m_data[indx] = val;

         m_size++;
     }
     
     /* Metode for å fjerne elementer fra arrayen */
     void remove(int indx){
         if (indx > m_size){
             throw out_of_range("Indek " + to_string(indx) + " uttafor.. igjen.");
         }
         for (int i = indx; i < m_size; i++){
             m_data[i] = m_data[i+1];
         }
         m_size--;
         if (m_size < 0.25*m_capacity){
             shrink_to_fit();
         }
     }

    /* Metode for å fjerne et element fra arrayen og returne verdien som ble slettet */
     int pop(int indx){
         if (indx > m_size){
             throw out_of_range("Indek " + to_string(indx) + " uttafor.. igjen.");
         }
         int element = m_data[indx];
         for (int i = indx; i < m_size; i++){
             m_data[i] = m_data[i+1];
         }
         m_size--;
         if (m_size < 0.25*m_capacity){
             shrink_to_fit();
         }
         return element;

     }

    /* Metode for å fjerne det siste elementet og returnere den slettede verdien */
     int pop(){
         int element = m_data[m_size-1];
         remove(m_size);
         return element;

     }

    /* Metode for å redusere kapasiteten til arrayen om man har fjernet en del elementer*/
     void shrink_to_fit(){
         int toer_potens = 2;
         while (toer_potens < m_size) {
             toer_potens *= 2;
         }
         m_capacity = toer_potens;
     }
};

