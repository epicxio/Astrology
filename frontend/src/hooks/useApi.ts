import { useState, useCallback } from 'react';
import { message } from 'antd';
import { useTranslation } from 'react-i18next';

interface UseApiOptions {
  showSuccessMessage?: boolean;
  successMessage?: string;
  showErrorMessage?: boolean;
  errorMessage?: string;
}

export function useApi<T>(
  apiFunction: (...args: any[]) => Promise<T>,
  options: UseApiOptions = {}
) {
  const { t } = useTranslation();
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const {
    showSuccessMessage = false,
    successMessage = t('common.success'),
    showErrorMessage = true,
    errorMessage = t('common.error'),
  } = options;

  const execute = useCallback(
    async (...args: any[]) => {
      try {
        setLoading(true);
        setError(null);
        const result = await apiFunction(...args);
        setData(result);
        if (showSuccessMessage) {
          message.success(successMessage);
        }
        return result;
      } catch (err) {
        const error = err as Error;
        setError(error);
        if (showErrorMessage) {
          message.error(errorMessage || error.message);
        }
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction, showSuccessMessage, successMessage, showErrorMessage, errorMessage]
  );

  return {
    data,
    loading,
    error,
    execute,
  };
}

// Example usage:
// const { data, loading, error, execute } = useApi(apiService.calculateHoroscope);
// const result = await execute(formData); 