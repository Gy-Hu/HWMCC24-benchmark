/*********************                                                        */
/*! \file
 ** \verbatim
 ** Top contributors (to current version):
 **   Makai Mann
 ** This file is part of the pono project.
 ** Copyright (c) 2019 by the authors listed in the file AUTHORS
 ** in the top-level source directory) and their institutional affiliations.
 ** All rights reserved.  See the file LICENSE in the top-level source
 ** directory for licensing information.\endverbatim
 **
 ** \brief
 **
 **
 **/

#pragma once

// use the header only implementation
#define FMT_HEADER_ONLY

#include <fmt/format.h>
#include <iostream>
#include <set>

#include <smt-switch/smt.h>

#define GLOG_NO_ABBREVIATED_SEVERITIES
#include <glog/logging.h>

#include "exceptions.h"

/****************************** Support for printing smt-switch objects
 * *********************************/

/** Takes a string and removes the curly brackets
 *  Since fmt/format.h uses {} to denote an argument
 *  it breaks if there are curly brackets in the string
 *  @param s the string to start with
 *  @return the same string but without curly brackets
 */
std::string remove_curly_brackets(std::string s);

// Term
template <>
struct fmt::formatter<smt::Term>
{
  template <typename ParseContext>
  constexpr auto parse(ParseContext & ctx)
  {
    return ctx.begin();
  }

  template <typename FormatContext>
  auto format(const smt::Term & t, FormatContext & ctx)
  {
    return format_to(ctx.out(), remove_curly_brackets(t->to_string()));
  }
};

// Sort
template <>
struct fmt::formatter<smt::Sort>
{
  template <typename ParseContext>
  constexpr auto parse(ParseContext & ctx)
  {
    return ctx.begin();
  }

  template <typename FormatContext>
  auto format(const smt::Sort & s, FormatContext & ctx)
  {
    return format_to(ctx.out(), remove_curly_brackets(s->to_string()));
  }
};

// PrimOp
template <>
struct fmt::formatter<smt::PrimOp>
{
  template <typename ParseContext>
  constexpr auto parse(ParseContext & ctx)
  {
    return ctx.begin();
  }

  template <typename FormatContext>
  auto format(const smt::PrimOp & po, FormatContext & ctx)
  {
    return format_to(ctx.out(), smt::to_string(po));
  }
};

// Op
template <>
struct fmt::formatter<smt::Op>
{
  template <typename ParseContext>
  constexpr auto parse(ParseContext & ctx)
  {
    return ctx.begin();
  }

  template <typename FormatContext>
  auto format(const smt::Op & o, FormatContext & ctx)
  {
    return format_to(ctx.out(), o.to_string());
  }
};

// Result
template <>
struct fmt::formatter<smt::Result>
{
  template <typename ParseContext>
  constexpr auto parse(ParseContext & ctx)
  {
    return ctx.begin();
  }

  template <typename FormatContext>
  auto format(const smt::Result & r, FormatContext & ctx)
  {
    return format_to(ctx.out(), r.to_string());
  }
};

/*********************** End overloaded methods for printing smt-switch objects
 * **********************/

/*************************************** Logger class
 * ************************************************/
// Meant to be used as a singleton class -- instantiated as logger below

namespace wasim {

class Log
{
 public:
  Log() : verbosity(0), verbosity_set(false) {}

  Log(size_t v) : verbosity(v), verbosity_set(true) {}

  /* Logs to the terminal using Python-style format string
   * @param level the verbosity level to print this log (prints for any
   * verbosity greater than this level)
   * @param format the format string
   * @param args comma separated list of inputs for the format string
   */
  template <typename... Args>
  void log(size_t level, const std::string & format, const Args &... args) const
  {
    if (level <= verbosity)
    {
      std::cout << fmt::format(format, args...) << std::endl;
    }
  }

  /* Logs to the terminal using Python-style format string in a range of
   * verbosities: [lower, upper]
   * @param lower the lower cutoff for verbosity
   * @param upper the upper cutoff for verbosity
   * @param format the format string
   * @param args comma separated list of inputs for the format string
   */
  template <typename... Args>
  void log(size_t lower,
           size_t upper,
           const std::string & format,
           const Args &... args) const
  {
    if ((lower <= verbosity) && (verbosity <= upper))
    {
      std::cout << fmt::format(format, args...) << std::endl;
    }
  }

  /* set verbosity -- can only be set once
   * @param v the verbosity to set
   */
  void set_verbosity(size_t v)
  {
    if (!verbosity_set)
    {
      verbosity = v;
    }
    else
    {
      throw SimulatorException("Can only set logger verbosity once.");
    }
  }

 protected:
  size_t verbosity;
  bool verbosity_set;
};

// globally avaiable logger instance
extern Log logger;

void set_global_logger_verbosity(size_t v);



// --------------------------------------------------------------------


// Only in Debug mode (Ignored in Release mode)
/******************************************************************************/
/// Log debug message to INFO if the "tag" has been enabled.
#define WASIM_DLOG(tag) DLOG_IF(INFO, DebugLog::Find(tag)) << "[" << tag << "] "

/// Log the message to INFO (lvl 0). (Debug)
#define WASIM_INFO DLOG(INFO)
/// Log the message to WARNING (lvl 1). (Debug)
#define WASIM_WARN DLOG(WARNING)
/// Log the message to ERROR (lvl 2). (Debug)
#define WASIM_ERROR DLOG(ERROR)
/// Conditionally log the message to INFO (lvl 0). (Debug)
#define WASIM_INFO_IF(b) DLOG_IF(INFO, b)
/// Conditionally log the message to WARNING (lvl 1). (Debug)
#define WASIM_WARN_IF(b) DLOG_IF(WARNING, b)
/// Conditionally log the message to ERROR (lvl 2). (Debug)
#define WASIM_ERROR_IF(b) DLOG_IF(ERROR, b)

/// Assertion with message logged to FATAL (lvl 3). (Debug)
#define WASIM_ASSERT(b) DLOG_IF(FATAL, !(b))

// Both in Debug and Release mode
// (Use only if high-assurance & non-performance critical)
/******************************************************************************/
/// Assertion with message logged to FATAL (lvl 3). (Debug/Release)
#define WASIM_CHECK(b) CHECK(b)
/// Assert equal with message logged to FATAL (lvl 3). (Debug/Release)
#define WASIM_CHECK_EQ(a, b) CHECK_EQ(a, b)
/// Assert not equal with message logged to FATAL (lvl 3). (Debug/Release)
#define WASIM_CHECK_NE(a, b) CHECK_NE(a, b)
/// Assert string equal with message logged to FATAL (lvl 3). (Debug/Release)
#define WASIM_CHECK_STREQ(a, b) CHECK_STREQ(a, b)
/// Assert point not NULL -- FATAL (lvl 3). (Debug/Release)
#define WASIM_NOT_NULL(ptr) CHECK_NOTNULL(ptr)

/// \brief Set the minimun log level.
/// Log messages at or above this level will be logged. (Default: 0)
/// - INFO: level 0
/// - WARNING: level 1
/// - ERROR: level 2
/// - FATAL: level 3
void SetLogLevel(const int& lvl);

/// \brief Set the path for log file.
/// If specified, logfiles are written into this directory instead of the
/// default logging directory (/tmp).
void SetLogPath(const std::string& path);

/// \brief Pipe log to stderr.
/// Log messages to stderr instead of logfiles, if set to 1.
void SetToStdErr(const int& to_err);

// Wrapper for debug tag log system.
/******************************************************************************/
/// A one-time class for initializing GLog.
class LogInitter {
public:
  /// Constructor to initialize GLog.
  LogInitter();
}; // class LogInitter

/// The wrapper for enabling and disabling debug tags.
class DebugLog {
public:
  /// Add a debug tag.
  static void Enable(const std::string& tag);

  /// Remove a debug tag.
  static void Disable(const std::string& tag);

  /// Clear all tags.
  static void Clear();

  /// Find if the tag is enabled.
  static bool Find(const std::string& tag);

private:
  /// The set of debug tags.
  static std::set<std::string> debug_tags_;

  /// The one and only initializer for the log system.
  static LogInitter init_;

}; // class DebugLog




}  // namespace wasim
