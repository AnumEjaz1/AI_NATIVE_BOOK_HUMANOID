import React from 'react';
import Layout from '@theme-original/Layout';
import { ProgressProvider } from '@site/src/contexts/ProgressContext';

export default function LayoutWrapper(props) {
  return (
    <ProgressProvider>
      <Layout {...props} />
    </ProgressProvider>
  );
}