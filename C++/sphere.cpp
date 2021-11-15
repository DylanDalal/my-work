// Name: Dylan Dalal
// FSUID: dmd19e
// Section: 010

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <iomanip>

#include "sphere.h"


Sphere::Sphere() {
    radius = 1;
    randomizeColor();
    color;
}

Sphere::Sphere(double r) {
    radius = r;
    randomizeColor();
    color;
}

Sphere::Sphere(double r, char c) {
    radius = r;
    toupper(c);
    if (c != 'B' && c != 'R' && c != 'P' && c != 'Y' && c != 'G' && c != 'L' && c != 'M')
        randomizeColor();
    else
        color = c;
}

double Sphere::getRadius() {
    return radius;
}

char Sphere::getColor() {
    return color;
}

double Sphere::getDiameter() {
    return radius * 2;
}

double Sphere::getSurfaceArea() {
    return (3.14159 * radius * radius * 4);
}

double Sphere::getVolume() {
    return (3.14159 * radius * radius * radius * 4) / 3;
}

void Sphere::setRadius(double r) {
    if (radius < 0)
        radius = r;
}

void Sphere::setColor(char c) {
    toupper(c);
    if (c == 'B' || c == 'R' || c == 'P' || c == 'Y' || c == 'G' || c == 'L' || c != 'M')
        color = c;
}

void Sphere::grow(double amount) {
    double test;
    test = radius + amount;
    if (test > 0) //what if they enter a negative? lol idk
        radius = test;
}

void Sphere::shrink(double amount) {
    double test;
    test = radius - amount;
    if (test > 0)
        radius = test;
}

void Sphere::randomizeColor() {
    char c  ;
    int newNumber = rand() % 7 + 1;
    switch (newNumber) {
        case 1:
            c = 'B';
            break;
        case 2:
            c = 'R';
            break;
        case 3:
            c = 'P';
            break;
        case 4:
            c = 'Y';
            break;
        case 5:
            c = 'G';
            break;
        case 6:
            c = 'L';
            break;
        case 7:
            c = 'M';
            break;
    }
    color = c;
}

void Sphere::printSummary(int precision = 2) {
    char colorName[10];
    if ((precision > 5) || (precision < 1))
        precision = 2;
    std::cout << std::fixed << std::setprecision(precision) << "Radius:\t\t\t" << getRadius() << "\n";
    std::cout << "Color:\t\t\t";
        //Color assignment through variety from the surprisingly-long switch statement!
        if(color=='B')
            std::cout<<"Blue";
        if(color=='R')
            std::cout<< "Red";
        if(color=='P')
            std::cout<<"Purple";
        if(color=='Y')
            std::cout<<"Yellow";
        if(color=='L')
            std::cout<<"Black";
        if(color=='M')
            std::cout<<"Maroon";
        if(color=='G')
            std::cout<<"Green";
    std::cout<<std::endl;
    std::cout << "Diameter:\t\t" << std::setprecision(precision) << getDiameter() << "\n";
    std::cout << "Volume:\t\t\t" << std::setprecision(precision) << getVolume() << "\n";
    std::cout << "Surface Area:\t" << std::setprecision(precision) << getSurfaceArea() << "\n";
}