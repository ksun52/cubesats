# based on https://gitlab.kitware.com/cmake/community/-/wikis/FAQ#can-i-do-make-uninstall-with-cmake
# per : https://gitlab.kitware.com/cmake/community/-/wikis/FAQ#what-is-its-license
#       The snippets on this wiki are provided under the same license. (BSD 3-clause)
#
# CMake - Cross Platform Makefile Generator
# Copyright 2000-2023 Kitware, Inc. and Contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# * Neither the name of Kitware, Inc. nor the names of Contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#D ATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Add uninstall target

cmake_policy(SET CMP0007 NEW)

if(NOT EXISTS "/home/pi/code/team-papa/comms/libiio/install_manifest.txt")
	message(FATAL_ERROR "Cannot find install manifest: /home/pi/code/team-papa/comms/libiio/install_manifest.txt")
endif()

file(READ "/home/pi/code/team-papa/comms/libiio/install_manifest.txt" files)
string(REGEX REPLACE "\n" ";" files "${files}")
foreach(file ${files})
	message(STATUS "Uninstalling $ENV{DESTDIR}${file}")
	if(IS_SYMLINK "$ENV{DESTDIR}${file}" OR EXISTS "$ENV{DESTDIR}${file}")
		exec_program(
			"/usr/bin/cmake" ARGS "-E remove \"$ENV{DESTDIR}${file}\""
			OUTPUT_VARIABLE rm_out
			RETURN_VALUE rm_retval
		)
		if(NOT "${rm_retval}" STREQUAL 0)
			message(FATAL_ERROR "Problem when removing $ENV{DESTDIR}${file}")
		else()
			# delete empty directories (if they are empty)
		        get_filename_component(dir ${file} DIRECTORY)
		        string(REPLACE "/" ";" dir_list ${dir})
		        list(LENGTH dir_list dir_len)
		        foreach(X RANGE ${dir_len})
				file(GLOB result LIST_DIRECTORIES true "${dir}/*")
				list(LENGTH result result_len)
				if (NOT result_len EQUAL 0)
					# if directory not empty, stop
					break()
				endif()
				message(STATUS "Removing empty directory: ${dir}")
				exec_program(
					"/usr/bin/cmake" ARGS "-E remove_directory ${dir}"
					OUTPUT_VARIABLE stdout
					RETURN_VALUE result
				)
				if(NOT "${result}" STREQUAL 0)
					message(FATAL_ERROR "Failed to remove directory: '${file}'.")
				endif()
				get_filename_component(dir ${dir} DIRECTORY)
			endforeach()
		endif()
	else(IS_SYMLINK "$ENV{DESTDIR}${file}" OR EXISTS "$ENV{DESTDIR}${file}")
		message(STATUS "File $ENV{DESTDIR}${file} does not exist.")
	endif()
endforeach()
