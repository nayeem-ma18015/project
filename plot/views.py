from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from sympy import sympify, symbols
from sympy.core.sympify import SympifyError
import numpy as np
import matplotlib.pyplot as plt
import io

def home(request):
    return render(request, 'plot/home.html')

def plot_equation(request):
    if request.method == 'POST':
        equation = request.POST.get('equation')
        try:
            # Parse and validate the equation
            x = symbols('x')
            expr = sympify(equation)

            # Generate x and y values
            x_vals = np.linspace(-10, 10, 500)
            y_vals = [float(expr.subs(x, val)) for val in x_vals]

            # Create the plot
            plt.figure()
            plt.plot(x_vals, y_vals, label=f'y = {equation}')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.grid()
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')

            # Save the plot to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)

            # Return the plot as an image response
            response = HttpResponse(img, content_type='image/png')
            response['Content-Disposition'] = 'inline; filename="plot.png"'
            return response

        except SympifyError:
            return JsonResponse({'error': 'Invalid mathematical equation.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

