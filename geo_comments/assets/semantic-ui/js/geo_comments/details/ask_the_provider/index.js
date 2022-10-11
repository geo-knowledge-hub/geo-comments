/*
 * This file is part of GEO-Comments.
 * Copyright (C) 2022 GEO Secretariat.
 *
 * GEO-Comments is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from 'react';
import ReactDOM from 'react-dom';

import { AskProviderApp } from '@geo-knowledge-hub/geo-comments-react';


/**
 * Getting data
 */
const askTheProviderDiv = document.getElementById("ask-provider-div");


/**
 * Render component
 */
export const renderComponent = (...args) => {
  if (askTheProviderDiv) {
    ReactDOM.render(
      <AskProviderApp
        record={JSON.parse(askTheProviderDiv.dataset.record)}
        userIsAuthenticated={JSON.parse(askTheProviderDiv.dataset.userIsAuthenticated)}
        defaultQueryParams={JSON.parse(askTheProviderDiv.dataset.defaultQueryConfig)}
      />,
      askTheProviderDiv
    );
  }
};
