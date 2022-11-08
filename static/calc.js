function calculator() {
    var user_input = document.getElementById("lift").value
    user_input = Number.parseFloat(user_input)
    var weight= (user_input - 45)/2
    const poss_weights = [45, 35, 25, 10, 5, 2.5]
    var weights_to_add = {"45":0, "35":0, "25":0, "10":0, "5":0, "2.5":0};

    console.log(user_input, weight, weights_to_add)

    function get_weights(weight) {
        for (let num of poss_weights) {
            console.log(num, ",", weight)
            if (weight < num) {
            }
            else {
                weight = weight - num
                weights_to_add[num] += 1
                console.log(weights_to_add)
            }

        if (weight > 0) {
            get_weights(weight)
        }
    }
    }
    if (weight > 0) {
        get_weights(weight)
    }
    
    weights_to_add = JSON.stringify(weights_to_add)
    document.getElementById("result").innerHTML = weights_to_add
}


// Python

// def calculator(request):

//     user_input = request.POST['user_input']
//     user_input = float(user_input)
//     weight_no_bar = (user_input-45)/2

//     poss_weights = (45, 35, 25, 10, 5, 2.5)
//     weights_to_add = {}

//     for weights in poss_weights:
//         weights_to_add[weights] = 0

//     def get_weights(weight_no_bar):
//         for num in poss_weights:
//             if weight_no_bar < num:
//                 pass
//             else:
//                 weight_no_bar = weight_no_bar - num
//                 weights_to_add[num] += 1
//                 break
        
//         if weight_no_bar > 0:
//             get_weights(weight_no_bar)

//     if weight_no_bar > 0:
//         get_weights(weight_no_bar)
//         return render(request, 'result.html', {'results': weights_to_add})
//     else:
//         return render(request, 'result.html', {'result': f'Use {user_input/2} lb dumbbells!'})