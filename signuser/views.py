from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages as messages
from .models import User, Meal
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from inference_sdk import InferenceHTTPClient
import requests
from .forms import UserForm
import json
from django.http import JsonResponse

# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated: 
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        username = request.POST.get('name')
        passw = request.POST.get('password')
        print(f"name:{username}, password:{passw}")
        try:
            userobj = User.objects.get(name=username)
        except:
            print('user not found')
            messages.error(request, 'User not found!')
            context = {'page':page}
            return render(request, 'signuser/login_register.html', context)
            
        userobj = authenticate(request, email=email, password=passw)
        if userobj is not None:
            if passw == userobj.password: 
                print('User Logged in!')
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, "Username or Password does not match!")
                print('password error')
        else:
            messages.error(request, "Username or Password does not match!")
    

    context = {'page':page}
    return render(request, 'signuser/login_register.html', context)



def registerPage(request):
    page = 'register'
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            user = form.save()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        else:
            messages.error(request, 'Invalid info!')

    context = {'page':page, 'form':form}
    return render(request, 'signuser/login_register.html', context)

@login_required(login_url='/login')
def dashboard(request):
    active = 'home'
    # try:
    meal_objs = Meal.objects.filter(user=request.user)
    print(meal_objs)

    user_obj = User.objects.get(username=request.user.username)
    carbos = user_obj.carbos if user_obj.carbos else 0
    protos = user_obj.protos if user_obj.protos else 0
    fatos = user_obj.fatos if user_obj.fatos else 0
    # except:
    #     meal_objs = []
    context = {'active':active, 'meal_objs':meal_objs, 'carbos':carbos, 'protos':protos, 'fatos':fatos}
    return render(request, 'signuser/home.html', context)

@login_required(login_url='/login')
def nutriNinja(request):
    active = 'nutrininja'
    user_obj = User.objects.get(username=request.user.username)
    carbos = user_obj.carbos if user_obj.carbos else 0
    protos = user_obj.protos if user_obj.protos else 0
    fatos = user_obj.fatos if user_obj.fatos else 0
    context = {'active':active, 'photo_path':None, 'photo_name':None, 'carbos':carbos, 'protos':protos, 'fatos':fatos}

    if request.method == 'POST':
        try:
            filesys = FileSystemStorage()
            food_snap = request.FILES['food_snap']

            upload_folder = 'food_snaps'
            static_upload_dir = os.path.join(settings.STATIC_ROOT, upload_folder)

            if not os.path.exists(static_upload_dir):
                os.makedirs(static_upload_dir)

            photo_path = os.path.join(static_upload_dir, food_snap.name)
            with open(photo_path, 'wb') as photo_file:
                for chunk in food_snap.chunks():
                    photo_file.write(chunk)
            
            context['photo_path'] = f'signuser/images/food_snaps/{food_snap.name}'
            context['photo_name'] = food_snap.name
            print(context['photo_path'], context['photo_name'])
            return render(request, 'signuser/food_upload.html', context)

        except:
            try:
                if request.method == 'POST':
                    food_name = request.POST['food_name']
                    photo_path = request.POST['photo_path']
                    nutri_info = request.POST['nuri_info']
                    # meal_obj = Meal.objects.create(photo_path=photo_path, food_name=food_name, nutri_info=nutri_info)
                    # meal_obj.save()
                    print(f"POST data: {food_name}, {nutri_info}, {photo_path}")
                    return HttpResponseRedirect(reverse('home'))

            except:
                upload_folder = 'food_snaps'
                static_upload_dir = os.path.join(settings.STATIC_ROOT, upload_folder)
                photo_name = request.POST['photo_name']
                photo_path = os.path.join(static_upload_dir, photo_name)

                CLIENT = InferenceHTTPClient(
                    api_url="https://detect.roboflow.com",
                    api_key="4TFLqpycRN0FG5gHvY2z"
                )

                result = CLIENT.infer(photo_path, model_id="nutracal-food-detection/1")
                pred_list = [preds['class'] for preds in result['predictions']]
                
                nutri_info = []
                cals = 0
                carbs = 0
                protein = 0
                fats = 0

                for pred in pred_list:
                    nutri_info_p = []
                    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(pred)
                    response = requests.get(api_url, headers={'X-Api-Key': 'A1cfrg+KFgSwryxMvIJEkg==FCgDY1rUKnE8ys9c'})

                    if response.status_code == requests.codes.ok:
                        response = response.json()
                        nutri_info_p.append(response[0]['calories'])
                        cals += round(response[0]['calories'])

                        nutri_info_p.append(response[0]['carbohydrates_total_g'])
                        carbs += round(response[0]['carbohydrates_total_g'])

                        nutri_info_p.append(response[0]['protein_g'])
                        protein += round(response[0]['protein_g'])

                        nutri_info_p.append(response[0]['fat_total_g'])
                        fats += round(response[0]['fat_total_g'])
                        
                        nutri_info.append(nutri_info_p)
                    else:
                        print("Error:", response.status_code, response.text)

                nutri_info_d = [cals, carbs, protein, fats]
                nutri_idx = ['cals', 'carbs', 'protein', 'fats']
                cal_r = round(nutri_info_d[0]*0.1)
                carb_r = round(nutri_info_d[1]*0.5)
                prot_r = round(nutri_info_d[2]*2)
                fat_r = round(nutri_info_d[3])
                nutri_val = [cal_r, carb_r, prot_r, fat_r]
                
                for i, val in enumerate(nutri_val):
                    if val > 10:
                        context[nutri_idx[i]] = nutri_val[i]
                    else:
                        context[nutri_idx[i]] = 0

                context['pred'] = pred_list
                context['nutri_info'] = nutri_info
                context['nutri_info_d'] = nutri_info_d
                context['pred_nut'] = list(zip(pred_list, nutri_info))
                context['photo_path'] = photo_path
                context['photo_name'] = photo_name
                context['result'] = result
                # context['rewards'] = rewards

                print(context)
                

    return render(request, 'signuser/food_upload.html', context)


def chat(request):
    active = 'chat'
    return None

@login_required(login_url='/login')
def profile(request):
    active = 'profile'
    username = request.user.username
    user_obj = User.objects.get(username=username)
    carbos = user_obj.carbos
    protos = user_obj.protos
    fatos = user_obj.fatos
    xp = user_obj.xp
    lvl = user_obj.level if user_obj.level else 1
    strength = user_obj.strength if user_obj.strength else 1
    muscle = user_obj.muscle if user_obj.muscle else 1
    physique = user_obj.physique if user_obj.physique else 1

    xp_dict = {1:500, 2:1000, 3:2000, 4:2500, 5:4000}
    stat_dict = {1:'Beginner', 2:'Intermediate', 3:'Pro', 4:'Master', 5:'Legend'}


    muscle_dict = {1:[200, 400, 800], 2:[350, 500, 700], 3:[500, 750, 1000], 4:[650, 800, 1200], 5:[900, 1500, 2000]}
    strength_dict = {1:[150, 300, 500], 2:[250, 550, 700], 3:[400, 700, 950], 4:[600, 850, 1100], 5:[750, 1000, 1500]}
    physique_dict = {1:[50, 75, 100], 2:[80, 100, 200], 3:[150, 200, 250], 4:[200, 250, 300], 5:[350, 500, 650]}

    next_xp_pts = xp_dict[lvl]
    user_stat = stat_dict[lvl]
    progress = round((xp/next_xp_pts)*100)
    
    protos_cost = muscle_dict[lvl][muscle-1]
    carbos_cost = strength_dict[lvl][strength-1]
    fatos_cost = physique_dict[lvl][physique-1]

    context = {'active':active, 'carbos':carbos, 'protos':protos, 'fatos':fatos, 'xp':xp, 'username':username, 'next_xp':next_xp_pts, 'user_stat':user_stat, 'lvl':lvl, 'nxt_lvl':lvl+1, 'progress':progress, 'protos_cost':protos_cost, 'carbos_cost':carbos_cost, 'fatos_cost':fatos_cost, 'muscle':muscle, 'strength':strength, 'physique':physique, 'stat':stat_dict[lvl]}
    return render(request, 'signuser/profile.html', context)


@login_required(login_url='/login')
def logMeal(request):
    print(f'entered...')
    if request.method == 'POST':
        data = eval(request.body.decode('ASCII'))
        result = data['result']
        food_name = ', '.join([preds['class'] for preds in result['predictions']])
        photo_name = data['photo_name']
        user_obj = request.user
        nutri_info_l = eval(data['nutri_info'])
        nutri_info_d = eval(data['nutri_info_d'])

        cals = nutri_info_d[0]
        carbs = nutri_info_d[0]
        protein = nutri_info_d[0]
        fats = nutri_info_d[0]

        print(f"POST data: {food_name}, {nutri_info_d}, {photo_name}")
        meal_obj = Meal.objects.create(user=user_obj, photo_name=photo_name, food_name=food_name, cals=cals, carbs=carbs, protein=protein, fats=fats)
        meal_obj.save()
        return HttpResponse(200)
    return None

@login_required(login_url='/login')
def getReward(request):
    if request.method == 'POST':
        data = eval(request.body.decode('ASCII'))
        carbo = int(data['carbo'])
        proto = int(data['proto'])
        fato = int(data['fato'])
        xp = int(data['xp'])

        xp_dict = {1:500, 2:1000, 3:2000, 4:2500, 5:4000}

        user_obj_name = request.user.username
        user_obj = User.objects.get(username=user_obj_name)

        if user_obj.carbos:
            user_obj.carbos += carbo
        else:
            user_obj.carbos = carbo

        if user_obj.protos:
            user_obj.protos += proto
        else:
            user_obj.protos = proto

        if user_obj.fatos:
            user_obj.fatos += fato
        else:
            user_obj.fatos = fato
        
        if user_obj.xp:
            user_obj.xp += xp
        else:
            user_obj.xp = xp

        user_obj.muscle = user_obj.muscle if user_obj.muscle else 1
        user_obj.strength = user_obj.strength if user_obj.strength else 1
        user_obj.physique = user_obj.physique if user_obj.physique else 1

        if user_obj.level:
            if user_obj.xp > xp_dict[user_obj.level]:
                user_obj.level += 1
                user.muscle = 1
                user.strength = 1
                user.physique = 1
        else:
            user_obj.level = 1
        
        user_obj.save()
        data = {'carbos':user_obj.carbos, 'protos':user_obj.protos, 'fatos':user_obj.fatos}
        data_json = json.dumps(data)
        print(data_json)
        return HttpResponse(data_json, content_type='application/json')

    return None

@login_required(login_url='/login')
def buyCategory(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        data = eval(request.body.decode('ASCII'))
        category = data['category']
        cost = int(data['cost'])
        lvl = user.level

        xp_dict = {1:500, 2:1000, 3:2000, 4:2500, 5:4000}
        
        if category == 'muscle':
            user.protos -= cost
            val = user.protos
            user.xp += 50
            if user.xp >= xp_dict[lvl]:
                user.level += 1
                user.xp = 0
            user.muscle = user.muscle + 1 if user.muscle < 3 else 3
            star = user.muscle


        elif category == 'strength':
            user.carbos -= cost
            val = user.carbos
            user.xp += 50
            if user.xp >= xp_dict[lvl]:
                user.level += 1
                user.xp = 0
            user.strength = user.strength + 1 if user.strength < 3 else 3
            star = user.strength
        
        elif category == 'physique':
            user.physique -= cost
            val = user.physique
            user.xp += 50
            if user.xp >= xp_dict[lvl]:
                user.level += 1   
                user.xp = 0 
            user.physique = user.physique + 1 if user.physique < 3 else 3
            star = user.physique

        else:
            print('error!')
            return None

        user.save()
        prog = round((user.xp/xp_dict[user.level])*100)

        data_json = json.dumps({'val':val, 'star':star, 'user_xp':user.xp, 'prog':prog})
        return HttpResponse(data_json, content_type='application/json')
    
    return None


def infoPage(request):
    pass



