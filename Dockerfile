FROM quay.io/astronomer/astro-runtime:6.0.4

#### Docker Customizations below this line ####

## This is te default directory where pyenv will be installed
## You can choose a different path as well
ENV PYENV_ROOT="/home/astro/.pyenv"
ENV PATH=${PYENV_ROOT}/bin:${PATH}

## install pyenv, install the required version
# pyenv virtualenv <pythono_version> <environment_name>
RUN curl https://pyenv.run | bash && \
    eval "${pyenv init -}" && \
    pyenv install 3.8.4 my_special_virtual_env && \
    pyenv activate my_special_virtual_env && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r my_special_requirements.txt
