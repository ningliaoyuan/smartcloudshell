#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals, print_function
import spacy
import plac
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token

# Custom pipeline components: https://spacy.io//usage/processing-pipelines#custom-components
azureResources = ['virtual machine']

class AzureResourceRecognizer(object):
    name = 'AzureResourceRecognizer'  # component name, will show up in the pipeline
    def __init__(self, nlp, label='AzureResource'):
        """Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the shared vocab, get the label ID and
        generate Doc objects as phrase match patterns.
        """
        self.label = nlp.vocab.strings[label]  # get entity label ID
        patterns = [nlp(org) for org in azureResources]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('AzureResource', None, *patterns)

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension('is_azure_resource', default=False)

        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_azure_resource == True.
        Doc.set_extension('has_azure_resource', getter=self.has_azure_resource)
        Span.set_extension('has_azure_resource', getter=self.has_azure_resource)

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and modify it if matches
        are found. Return the Doc, so it can be processed by the next component
        in the pipeline, if available.
        """
        matches = self.matcher(doc)
        spans = []  # keep the spans for later so we can merge them afterwards
        for _, start, end in matches:
            # Generate Span representing the entity & set label
            entity = Span(doc, start, end, label=self.label)
            spans.append(entity)
            # Set custom attribute on each token of the entity
            for token in entity:
                token._.set('is_azure_resource', True)
            # Overwrite doc.ents and add entity – be careful not to replace!
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token. This is done
            # after setting the entities – otherwise, it would cause mismatched
            # indices!
            span.merge()
        return doc  # don't forget to return the Doc!

    def has_azure_resource(self, tokens):
        """Getter for Doc and Span attributes. Returns True if one of the tokens
        is a tech org. Since the getter is only called when we access the
        attribute, we can refer to the Token's 'is_azure_resource' attribute here,
        which is already set in the processing step."""
        return any([t._.get('is_azure_resource') for t in tokens])
