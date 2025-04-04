from django.shortcuts import render

# Create your views here.
# tasks/views.py
from django.shortcuts import render, redirect
from .models import Task
from django.utils.timezone import localtime, now

def home(request):
    return render(request,'home.html')


def task_list(request):
    today = localtime(now()).date()  # Get today's date
    tasks = Task.objects.filter(created_date__date=today)  # Filter tasks for today
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        
        Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'tasks/add_task.html')

def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')



import calendar
import json
from django.shortcuts import render
from django.utils.timezone import localtime, now
from .models import Task

def calendar_view(request):
    today = localtime(now()).date()
    year, month = today.year, today.month
    month_name = calendar.month_name[month]

    print(f"\n🔵 DEBUG: Year = {year}, Month = {month}")

    # Get all tasks for the month
    tasks = Task.objects.filter(created_date__year=year, created_date__month=month)
    tasks_by_date = {}

    print(f"\n🔵 DEBUG: Found {len(tasks)} tasks for {month_name}")

    for task in tasks:
        task_date = task.created_date.date()
        print(f"🔹 Task: {task.title}, Date: {task_date}, Completed: {task.completed}")

        if task_date not in tasks_by_date:
            tasks_by_date[task_date] = []
        tasks_by_date[task_date].append({"title": task.title, "completed": task.completed})

    # Generate calendar structure
    month_calendar = []
    cal = calendar.Calendar()
    for week in cal.monthdatescalendar(year, month):
        week_data = []
        for day in week:
            if day.month == month:
                day_tasks = tasks_by_date.get(day, [])  # Get tasks for that day
                is_completed = all(task["completed"] for task in day_tasks) if day_tasks else False
                
                print(f"🗓 Processing Day: {day}, Completed: {is_completed}, Tasks: {day_tasks}")

                week_data.append({
                    "day": day.day,
                    "completed": is_completed,
                    "tasks": json.dumps(day_tasks)  # Convert task list to JSON
                })
            else:
                week_data.append(None)  # Empty cell for other months
        month_calendar.append(week_data)

    print(f"\n🔵 DEBUG: Final month_calendar = {month_calendar}")

    return render(request, 'tasks/calender.html', {
        "month_name": month_name,
        "year": year,
        "month_calendar": month_calendar,
    })
