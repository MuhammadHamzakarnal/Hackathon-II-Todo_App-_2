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

# Verify bcrypt version - Build timestamp: 2026-01-29T12:11
# bcrypt 4.0.1 is the last version with __about__ module for passlib compatibility
RUN python -c "import bcrypt; print('bcrypt version:', bcrypt.__version__); assert bcrypt.__version__ == '4.0.1', f'Expected bcrypt 4.0.1, got {bcrypt.__version__}'"

COPY --chown=user . /app

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--reload"]