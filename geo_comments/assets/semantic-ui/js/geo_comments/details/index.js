/*
 * This file is part of GEO-Comments.
 * Copyright (C) 2022 GEO Secretariat.
 *
 * GEO-Comments is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from 'react';

// Factorizing
const renderFactory = async (componentsAvailable) => {
  await componentsAvailable.forEach(async (componentName) => {
    const componentModule = await import(`./${componentName}`);
    componentModule.renderComponent();
  });
};

// Importing the components
const componentsAvailable = [
  'ask_the_provider',
  'feedback_space'
];

renderFactory(componentsAvailable);
