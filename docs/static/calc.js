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