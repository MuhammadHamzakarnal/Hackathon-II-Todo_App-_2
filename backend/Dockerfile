FROM python:3.9-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Verify that pydantic-settings is installed
RUN python -c "import pydantic_settings; print('pydantic_settings version:', pydantic_settings.__version__)"

# Verify bcrypt version (force rebuild on version change) - Build timestamp: 2026-01-29T11:52:40
RUN python -c "import bcrypt; print('bcrypt version:', bcrypt.__version__); assert int(bcrypt.__version__.split('.')[0]) < 4, 'bcrypt 4.x not supported'"

COPY --chown=user . /app

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--reload"]