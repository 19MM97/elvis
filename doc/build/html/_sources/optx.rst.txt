optx module
===========

.. automodule:: optx
   :members: 
   :undoc-members:
   :show-inheritance: 

   ..  method:: power_bounds_rule(mod, i)
   
       Define power limits for each car.
 
       :param mod: Pyomo optimization model.
       :param i: Model instance index.
       :type i: int
       :return: Upper and lower power limits for the charging power.
  
   .. method:: trafo_limit_rule(mod, j)
   
      Limit the total charging power to the maximal transformer load for each time step.

      :param mod: Pyomo optimization model.
      :param j: Model instance index.
      :param j: int
      :return: Maximal charging power.

   .. method:: demand_rule(mod, i)
   
      Adjust vehicle energy demand based on either parking time and maximal charging power or SOC target.

      :param mod: Pyomo optimization model.
      :param i: Model instance index.
      :type i: int
      :return: Energy demand.

   .. method:: objective_rule(mod)
   
      Target function to be minimized or maximized in order to optimize the charging plan.

      :param mod: Pyomo optimization model.
      :return: Target function.









