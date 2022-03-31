
$(function(){
    $('#add-button').on('click', function(e){
        e.preventDefault()
        let qty = $('#qty').val()
        let measure = $('#measure').val()
        let ingredient = $('#ingredient').val()
        let department = $('#department').val()
        if(qty != "0" && measure != "" && ingredient != ""){
            let new_row = `
            <tr>
            <td>${qty}</td>
            <td>${measure}</td>
            <td>${ingredient}</td>
            <td style='display:none'>${department}</td>
            </tr>`
            $('#ingredient_list > tbody').append(new_row)
        }
    })
    $('.card').on('click', function(){
        let recipe_id = $(this).children('input').val()
        $.post('/get_recipe_by_id', {"id":recipe_id}, function(response){
            $('')

        })
    })

    $('#save-recipe-button').on('click', function(e){
        e.preventDefault()
        let form_data = new FormData($('#add-recipe-form')[0]);
        let categories = $('#category').val()
        for(var i = 0; i < categories.length; i++){
            form_data.append(`cat_${i+1}`, categories[i])
        }
        var ingredient_num = 1
        $('#ingredient_list tr').each(function(){
            var row = $(this);
            form_data.append(`ing_${ingredient_num}_qty`, row.find("td:eq(0)").text());
            form_data.append(`ing_${ingredient_num}_measure`, row.find("td:eq(1)").text());
            form_data.append(`ing_${ingredient_num}`, row.find("td:eq(2)").text());
            form_data.append(`ing_${ingredient_num}_department`, row.find("td:eq(3)").text());
            ingredient_num++
        })
        $.ajax({
            url: "/add_recipe",
            data: form_data,
            cache: false,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function (response) {
                console.log(response);
                console.log("success");
            }
        })
        $('#add_recipe_modal').foundation('close');
        
    });
    $('#disp_category').on('change', function(){
        $('#recipe_box .cell').remove()
        let data = {"id":$(this).val()}
        
        if(data.id == "all"){
            $.post('/get_all_recipes', function(response){
                var resp = JSON.parse(response)
                Object.entries(resp).forEach((entry) => {
                    const [key, value] = entry;
                    new_markup = `
                        <div class=\"cell\">
                            <div class=\"card\">
                                <input type=\'hidden\' value=\'${value.id}\'>
                                <div class=\"card-section\">
                                    <img src=\"/static/assets/images/food_placeholder.jpg\">
                                </div>
                                <div class=\"card-section padding-top-0\">
                                    <div class=\"grid-x align-center\">
                                        <span class=\"recipe-card\">${value.name}</span>
                                    </div>
                                    <div class=\"grid-x align-center\">
                                        <span class=\"recipe-card\">Cooks in: ${value.cook_time}min</span>
                                    </div>
                                    <div class=\"grid-x align-center\">
                                        <span class=\"recipe-card\">
                                            <i class=\"fa-solid fa-star\"></i>
                                            <i class=\"fa-solid fa-star\"></i>
                                            <i class=\"fa-solid fa-star\"></i>
                                            <i class=\"fa-solid fa-star\"></i>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>`
                    $('#recipe_box').append(new_markup)
                });

            });
            
        }
        else {
            $.post('/get_recipes_by_category', data, function(response){
                var resp = JSON.parse(response)
                Object.entries(resp).forEach((entry) => {
                    const [key, value] = entry;
                    new_markup = `
                        <div class=\"cell\">
                            <div class=\"card\" data-open=\"recipe_modal\">
                                <input type=\'hidden\' value=\'${value.id}\'>
                                <div class=\"card-section\">
                                    <img src=\"/static/assets/images/food_placeholder.jpg\">
                                </div>
                                <div class=\"card-section padding-top-0\">
                                    <div class=\"grid-x align-center\">
                                        <span class=\"recipe-card\">${value.name}</span>
                                    </div>
                                    <div class=\"grid-x align-center\">
                                        <span class=\"recipe-card\">Cooks in: ${value.cook_time}min</span>
                                    </div>
                                    <div class=\"grid-x align-center\">
                                        <span class=\"recipe-card\">
                                            <i class=\"fa-solid fa-star\"></i>
                                            <i class=\"fa-solid fa-star\"></i>
                                            <i class=\"fa-solid fa-star\"></i>
                                            <i class=\"fa-solid fa-star\"></i>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>`
                    $('#recipe_box').append(new_markup)
                });
            })
        }
    })
})