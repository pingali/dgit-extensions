

*Note: This repo has been just created. It will get cleaned up
over the next few days. Please dont use it yet.* 

`dgit <https://github.com/pingali/dgit>`_ is a dataset management
tool. This repo has a series of dgit addons that are expected to be
more computationally expensive/otherwise complex such as integrity
checks, anonymization, and may be eventually bitcoin integration.

::

   $ pip install dgit-extensions 

   # The modules in bold are extensions from this repo 
   $ dgit plugins 
   ========
   metadata
   ========
   generic-metadata (v0) : generic-metadata Basic metadata tracker
      Supp: ['generic-metadata']
   
   ========
   validator
   ========
   basic-validator (v0) : basic-validator Basic validator of the content
      Supp: ['basic-validator']
   **simple-validator (v0) : simple-validator Simple validator extension
      Supp: ['simple-validator']**
   
   ========
   instrumentation
   ========
   platform (v0) : platform Execution platform information
      Supp: ['platform']
   content (v0) : content Basic content analysis
      Supp: ['content']
   executable (v0) : executable Executable analysis
      Supp: ['executable']
   
   ========
   backend
   ========
   s3 (v0) : s3 S3 backend
      Supp: ['s3']
   local (v0) : local Local filesystem backend
      Supp: ['local']
   
   ========
   repomanager
   ========
   git (v0) : git Git-based repomanager
      Supp: ['git']
      
   


Validator 
=========

This will evaluate the content against the validation rules specified
