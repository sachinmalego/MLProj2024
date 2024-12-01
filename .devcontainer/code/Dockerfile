FROM python:3.11.4-bookworm

WORKDIR /base

# Install required Python packages
RUN pip3 install dash
RUN pip3 install pandas
RUN pip3 install dash_bootstrap_components
RUN pip3 install dash-bootstrap-components[pandas]
RUN pip3 install numpy
RUN pip3 install scikit-learn
RUN pip3 install plotly

# Testing modules
RUN pip3 install dash[testing]
RUN pip3 install pytest
RUN pip3 install pytest-depends

# Copy application code
COPY . /base

# Keep container running (can be replaced with specific CMD if needed)
CMD tail -f /dev/null
