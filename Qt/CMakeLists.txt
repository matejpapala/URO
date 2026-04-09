cmake_minimum_required(VERSION 3.16)
project(EventPlanner LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(EventPlanner
    main.cpp
    app.h app.cpp
    monthview.h monthview.cpp
    addeventview.h addeventview.cpp
    eventdetailsview.h eventdetailsview.cpp
    datepickerpopup.h datepickerpopup.cpp
)

target_link_libraries(EventPlanner PRIVATE Qt6::Widgets)
