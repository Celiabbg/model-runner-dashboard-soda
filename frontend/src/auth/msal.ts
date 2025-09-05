export const msalConfig = {
  auth: {
    clientId: import.meta.env.VITE_AAD_CLIENT_ID ?? 'YOUR-CLIENT-ID',
    authority: `https://login.microsoftonline.com/${import.meta.env.VITE_AAD_TENANT_ID ?? 'common'}`,
    redirectUri: typeof window !== 'undefined' ? window.location.origin : '',
  }
};