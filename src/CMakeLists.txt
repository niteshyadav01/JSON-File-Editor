set(APP_NAME todo_app)
set(MAIN_SCRIPT main.py)
get_filename_component(MAIN_SCRIPT_NAME ${MAIN_SCRIPT} NAME_WE)

file(GLOB_RECURSE UI_FILES 
    ${CMAKE_CURRENT_SOURCE_DIR}/*.ui
    ${CMAKE_SOURCE_DIR}/plugins/*.ui
    ${CMAKE_SOURCE_DIR}/plugins/*/*.ui
)

file(GLOB_RECURSE QRC_FILES 
    ${CMAKE_CURRENT_SOURCE_DIR}/*.qrc
    ${CMAKE_SOURCE_DIR}/plugins/*.qrc
    ${CMAKE_SOURCE_DIR}/plugins/*/*.qrc
)

set(GENERATED_UI_FILES "")
set(GENERATED_QRC_FILES "")

add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/auto_gen
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/auto_gen
)

foreach(UI_FILE ${UI_FILES})
    get_filename_component(UI_NAME ${UI_FILE} NAME_WE)
    set(UI_PY_FILE ${UI_NAME}_ui.py)

    add_custom_command(
        OUTPUT ${UI_PY_FILE}
        COMMAND pyside6-uic ${UI_FILE} -o ${CMAKE_BINARY_DIR}/auto_gen/${UI_PY_FILE}
        DEPENDS ${UI_FILE} ${CMAKE_BINARY_DIR}/auto_gen
        COMMENT "Compiling ${UI_FILE} → ${CMAKE_BINARY_DIR}/auto_gen/${UI_NAME}_ui.py"
    )

    list(APPEND GENERATED_UI_FILES ${UI_PY_FILE})
endforeach()

foreach(QRC_FILE ${QRC_FILES})
    get_filename_component(QRC_NAME ${QRC_FILE} NAME_WE)
    set(QRC_PY_FILE ${QRC_NAME}_rc.py)

    add_custom_command(
        OUTPUT ${QRC_PY_FILE}
        COMMAND pyside6-rcc ${QRC_FILE} -o ${CMAKE_BINARY_DIR}/auto_gen/${QRC_PY_FILE}
        DEPENDS ${QRC_FILE} ${CMAKE_BINARY_DIR}/auto_gen
        COMMENT "Compiling ${QRC_FILE} → ${CMAKE_BINARY_DIR}/auto_gen/${QRC_NAME}_rc.py"
    )

    list(APPEND GENERATED_QRC_FILES ${QRC_PY_FILE})
endforeach()

add_custom_target(${APP_NAME} ALL
    DEPENDS ${GENERATED_UI_FILES} ${GENERATED_QRC_FILES}

    COMMAND pyinstaller
        ${MAIN_SCRIPT}
        --name ${APP_NAME}
        --noconsole
        --paths=${CMAKE_BINARY_DIR}/auto_gen/ 
        --paths=${CMAKE_SOURCE_DIR}/libs
        --paths=${CMAKE_SOURCE_DIR}/plugins
        --distpath=${CMAKE_BINARY_DIR}/run/
        --clean
        --noconfirm
        --onedir

    COMMAND ${CMAKE_COMMAND} -E rm -f ${CMAKE_CURRENT_SOURCE_DIR}/${APP_NAME}.spec
    COMMAND ${CMAKE_COMMAND} -E rm -fr ${CMAKE_CURRENT_SOURCE_DIR}/build
    
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Building PyQt App with Nuitka"
)

add_custom_command( TARGET ${APP_NAME}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_SOURCE_DIR}/run/bin
    COMMENT "Create ${CMAKE_SOURCE_DIR}/run/bin folder."
)   

add_custom_command(TARGET ${APP_NAME}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_BINARY_DIR}/run/${APP_NAME} ${CMAKE_SOURCE_DIR}/run/bin
    COMMENT "Copying ${APP_NAME} to run/bin/ folder."
)