## how to start?
* install python 3.6.2
* clone this repository
* open console inside cloned repository: \
pip install -r requirements.txt
* run main file from console: \
python main.py
## how it works?
![example after evaluation](./figure.png)
1) Naive approach:
    * use cross section of curve and circle with constant radius \
    to find out next point
    * parameter step calibration

   this approach has several disadvantages:
    * breaks of function
    * too small or too big parameter step (f.e. y = 1/x) \
    when step of parameter of function can't be changed because \
    the accuracy of float type can't be increased
    * you can't predict start step of parameter \
    (f.e.: t=0..1, function: f(t) = 1/t, step of t = 0.1. In this case \
    you have only a few points which describes only tail of the function)

   advantages:
    * only for very small step and small changes of deferential of the function
    * very good accuracy when previous conditions is valid
2) Correct approach:
    * do sampling with constant step of parameter: \
    it removes breaks of function and you can increase speed for cases \
    when small change of parameter does not dramatically change  \
    the length of the curve
    * calculate length between each couple of points
   (in this example - linear interpolation)
   * calculate integral by length of segments: \
   sum segments length and calculate middle point on the line when achieve \
   constant segment length

   disadvantages:
   * slow for huge amount of points (because of sampling)
   * if you want something like sin(1/t) - you should use spline interpolation \
   and analytically solve the integral equation for your interpolation
   * |integral(f(t)-interpolated_f(t))|, t=t0..t0+step must goes to zero

   advantages:
   * custom optimization
   * predictable behavior
   * ignore breaks of function
   * can be used for all type of parametric functions
## how to configure?
Use input.py for setup functions fx(t) and fy(t). Setup interpolation step, \
segment length, and max count of points for output

