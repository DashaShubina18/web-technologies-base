from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from src.database import Base


item_tag = Table(
    "item_tag",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)

    items = relationship("Item", back_populates="owner")

    profile = relationship("Profile", back_populates="user", uselist=False)

    posts = relationship("Post", back_populates="author")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="profile")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    content = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    detail = relationship("Detail", uselist=False, back_populates="item")
    tags = relationship("Tag", secondary=item_tag, back_populates="items")


class Detail(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), index=True)
    item_id = Column(Integer, ForeignKey("items.id"), unique=True)

    item = relationship("Item", back_populates="detail")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)

    items = relationship("Item", secondary=item_tag, back_populates="tags")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))

    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )


def init_db(db):
    if not db.query(User).first():
        user1 = User(name="admin")
        user2 = User(name="guest")
        user3 = User(name="john")

        db.add_all([user1, user2, user3])
        db.commit()


    john = db.query(User).filter(User.name == "john").first()

    if john and not db.query(Profile).filter(Profile.user_id == john.id).first():
        profile = Profile(bio="Backend dev", user=john)
        db.add(profile)
        db.commit()

    if john and not db.query(Post).first():
        post1 = Post(
            title="First post",
            content="This is the first post",
            author=john
        )

        post2 = Post(
            title="Second post",
            content="This is the second post",
            author=john
        )

        db.add_all([post1, post2])
        db.commit()

    if not db.query(Item).first():
        item1 = Item(name="Sample Item 1", owner_id=1)
        item2 = Item(name="Sample Item 2", owner_id=2)

        db.add_all([item1, item2])
        db.commit()

    if not db.query(Tag).first():
        tag1 = Tag(name="Important")
        tag2 = Tag(name="Optional")

        db.add_all([tag1, tag2])
        db.commit()

    if not db.query(Student).first():
        course1 = Course(title="Python Basics")
        course2 = Course(title="Database Design")
        course3 = Course(title="Web Technologies")

        student1 = Student(name="Alice", courses=[course1, course2])
        student2 = Student(name="Bob", courses=[course1, course3])

        db.add_all([course1, course2, course3, student1, student2])
        db.commit()

    print("Database initialized with ORM relationships.")