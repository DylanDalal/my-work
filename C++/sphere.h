// Name: Dylan Dalal
// FSUID: dmd19e
// Section: 010

#ifndef SPHERE_H
#define SPHERE_H

class Sphere {
    private:
        double radius;
        char color;
    public:
        Sphere();
        Sphere(double radius);
        Sphere(double radius, char color);

        double getRadius();
        char getColor();
        double getDiameter();
        double getSurfaceArea();
        double getVolume();

        void randomizeColor();
        void grow(double amount);
        void shrink(double amount);
        void setRadius(double radiusTwo);
        void setColor(char colorTwo);
        void printSummary(int precision);
};

#endif