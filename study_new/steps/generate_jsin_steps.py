from steps import support_steps

#Create json for method POST /pet with required parameters
def create_json_post_pet_required_params():
    request = {}
    request ['name'] = support_steps.generate_random_letter_str(6)
    request ['photoUrls'] = ['photosberCat']
    print('request =', request)
    return request

#App json for method POST /pet with required parameters
def create_json_post_pet_all_params():
    request = {}
    request ['name'] = support_steps.generate_random_letter_str(6)
    request ['photoUrls'] = ['photosberCat']
    request ['category'] = {}
    request ['category'] ['name'] = support_steps.generate_random_letter_str(5)
    request ['tags'] = [{}]
    request ['tags'] [0] ['name'] = support_steps.generate_random_letter_str(5)
    request ['status'] = 'available'
    print('request =', request)
    return request