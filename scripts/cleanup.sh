#!/bin/bash

# Exit on any error
set -e

if [ -d "build" ]; then
    echo "🗑️  Removing build"
    rm -rf "build"
fi

if [ -d "dist" ]; then
    echo "🗑️  Removing dist"
    rm -rf "dist"
fi

if [ -d "roob.egg-info" ]; then
    echo "🗑️  Removing roob.egg-info"
    rm -rf "roob.egg-info"
fi