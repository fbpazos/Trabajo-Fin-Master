FROM jupyter/minimal-notebook

# Install "BNumMet" using PIP
RUN pip install BNumMet voila jupyterlab-mathjax3 mathjax

# Copy the notebooks into the container
ADD --chown=jovyan:users ./Demos/*.ipynb /home/jovyan/Demos/ 
ADD --chown=jovyan:users . /home/jovyan/BNumMet/ 
# Remove "work" directory
RUN rm -rf /home/jovyan/work


# Remove Jupyters password and token
RUN echo 'c.NotebookApp.token = ""' >> /home/jovyan/.jupyter/jupyter_notebook_config.py
RUN echo 'c.NotebookApp.password = ""' >> /home/jovyan/.jupyter/jupyter_notebook_config.py
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix





