from fastapi import FastAPI, HTTPException, status
from typing import Union, Optional
from pydantic import BaseModel # FOR CREATE AND UPDATE

app = FastAPI()

# DEFINE THE MODEL
class Course(BaseModel):
    title: str
    teacher: str
    students: Optional[list[str]]
    level: str


courses = {
    1: {
        "title": "Modern History",
        "teacher": "Ms. Doe",
        "students": ["Harry Potter", "Frodo Baggins"],
        "level": "advance"
    },
    2: {
        "title": "Mathematics",
        "teacher": "Mr. Davies",
        "students": ["John", "Sam"],
        "level": "intermediate"
    },
    3: {
        "title": "Geography",
        "teacher": "Ms. Apple",
        "students": ['Michael Jordan', "Bruce Lee"],
        "level": "beginner"
    }
}

@app.get("/api/hello/")
def hello_world():
    return {"message": "Hello world"}

@app.get('/api/courses/')
def get_courses(level: Union[str, None] = None):
    if level:
        level_courses = []
        for index in courses.keys():
            if courses[index]["level"] == level:
                level_courses.append(courses[index])
        return level_courses
    return courses

@app.get('/api/courses/{course_id}')
def get_course(course_id: int):
    try:
        return courses.get(course_id)
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Course with id: {course_id} not found"
        )
        
@app.delete('/api/courses/{course_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    try:
        del courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Course with id: {course_id} not found"
        )
        
@app.post('/api/courses/')
def create_course(new_course: Course):
    course_id = max(courses.keys()) + 1
    courses[course_id] = new_course.dict()
    return courses[course_id]

@app.put('/api/courses/{course_id}')
def update_course(updated_course: Course, course_id: int):
    try:
        course = courses[course_id]
        course["title"] = updated_course.title
        course["teacher"] = updated_course.teacher
        course["students"] = updated_course.students
        course["level"] = updated_course.level
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Course id: {course_id} not found."
        )