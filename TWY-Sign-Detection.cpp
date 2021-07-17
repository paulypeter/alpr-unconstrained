#include <iostream>
#include "TWY-Sign-Detection.h"
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>

struct SignText {
    std::string current;
};

SignText TwySignDetector::getSignText() {
    SignText res;
    return res;
};