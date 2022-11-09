---
title: Lift Calculator in Javascript
author: Chris
date: 11/09/2022
tags: code, python, javascript
---

I'd classify myself as mediocre as a Python developer. I'm more of a scripter, really. Automating tasks in Python has been pretty fun over the last year and half or so.

But as I've gotten more into web stuff, Javascript keeps staring me in the face, and I've avoided it up until now. If my Python is mediocre, my Javascript ability is best classified as *complete and utter novice*. That's fine... I'm not planning on being a full-blown Javascript developer, and upon reading and listening to a lot about internet bloat, I'll probably mostly stay away from it.

But! A few months ago, out of frustration from calculating the weights I needed on the bar for lifting, I built a weightlifting calculator in Python and hosted it on [PythonAnywhere](http://cdbaca.pythonanywhere.com/weightlifting/) (I doubt if this link will stay live forever, but this is it for now.)

The problem is, as far as I'm aware, I can't do server-side scripting on the static site generator I've got going on here. The thought then became, can I move the calculator over to this site and use client-side scripting with Javascript? Turns out you can!

The Python code was simple:

`

    def calculator(request):

        user_input = request.POST['user_input']
        user_input = float(user_input)
        weight_no_bar = (user_input-45)/2

        poss_weights = (45, 35, 25, 10, 5, 2.5)
        weights_to_add = {}

        for weights in poss_weights:
            weights_to_add[weights] = 0

        def get_weights(weight_no_bar):
            for num in poss_weights:
                if weight_no_bar < num:
                    pass
                else:
                    weight_no_bar = weight_no_bar - num
                    weights_to_add[num] += 1
                    break
            
            if weight_no_bar > 0:
                get_weights(weight_no_bar)

        if weight_no_bar > 0:
            get_weights(weight_no_bar)
            return render(request, 'result.html', {'results': weights_to_add})
        else:
            return render(request, 'result.html', {'result': f'Use {user_input/2} lb dumbbells!'})

`

It takes the post request from the form, does some math, and returns a dictionary object to the html page. Then the template form parses the dictionary renders the data.

I've transferred the logic to Javascript (probably poorly, as I barely understand the syntax... all these brackets, ugh!). Here's the same-ish logic in Javascript:

`

    function calculator() {
        document.getElementById("result").innerHTML = '';
        let user_input = document.getElementById("lift").value
        user_input = Number.parseFloat(user_input)
        let weight= (user_input - 45)/2
        const poss_weights = [45, 35, 25, 10, 5, 2.5]
        let weights_to_add = {"45":0, "35":0, "25":0, "10":0, "5":0, "2.5":0};

        function get_weights(weight) {
            for (let num of poss_weights) {
                if (weight < num) {
                }
                else {
                    weight = weight - num
                    weights_to_add[num] += 1
                    break
                }
            }
            if (weight > 0) {
                get_weights(weight)
        }
        }
        if (weight > 0) {
            get_weights(weight)
        }
        
        for (let key of poss_weights) {
            document.getElementById("result").innerHTML += `<li><h5>${key}: ${weights_to_add[key]}</h5></li>`;
        }
    }

`

What's cool about this is that when the JS function runs, it deletes whatever content is in the html "results" tag, then runs the logic as before, then lists the weights and amounts in order for what needs to be put on the bar.

[Here's the link](../docs/lift.html) to the lift calculator on the SSG.

Not the best thing ever, and it can probably be cleaned up design-wise, but this was one of my goals when redesigning this site. I'm happy with it!
