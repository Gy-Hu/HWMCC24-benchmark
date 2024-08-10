#include <frontend/smt_in.h>
#include <utils/exceptions.h>

namespace wasim
{
  
WasimSmtLib2Parser::WasimSmtLib2Parser(const std::string & filename,
                                     smt::SmtSolver & solver)
    : super(solver), filename_(filename)
{
  set_logic_all();
  int res = parse(filename_);
  assert(!res);  // 0 means success
}

smt::Term WasimSmtLib2Parser::register_arg(const std::string & name,
                                          const smt::Sort & sort)
{
  smt::Term tmpvar;
  try {
    tmpvar = solver_->get_symbol(name);
  }
  catch (const std::exception & e) {
    // cout << "ERROR: Could not find " << name << " in solver! Wrong input
    // value."<< endl; cout << sort->get_sort_kind() << endl;
    tmpvar = solver_->make_symbol(name, sort);
  }
  arg_param_map_.add_mapping(name, tmpvar);
  return tmpvar;  // we expect to get the term in the transition system.

  // TODO: symbolic values do not exist in the transition system
}

smt::Term WasimSmtLib2Parser::return_defs()
{
  for (const auto & d : defs_)
    // cout << d.first << " : " << d.second << endl;
    return d.second;
  throw SimulatorException("No function definitions loaded so far");
  return NULL;
}


} // namespace wasim
