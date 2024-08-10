// lib.h
// Synopsis: the header of the simple library

#ifndef SIMPLE_LIB_H__
#define SIMPLE_LIB_H__


#include <ilang/ilang++.h>

/// \brief the class to build a pipe's model
class SimplePipe {

public:
  static ilang::Ila BuildModel();
  static ilang::Ila BuildStallModel();

}; // class SimplePipe

#endif // SIMPLE_LIB_H__

