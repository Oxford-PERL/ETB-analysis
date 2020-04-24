# a PERLite's guide to GitHub and contributing to the PERL repo
(written for those who are new to using github)

## Add new members to the Oxford-PERL Organisation (Oxford-PERL Owners only)
1. New contributors to this repository should first be added to the Oxford-PERL Organisation. The organisation owner should follow [this guide](https://help.github.com/en/enterprise/2.16/user/github/setting-up-and-managing-organizations-and-teams/adding-people-to-your-organization) to add new members to the organisation.
2. Once the invitation has been accepted, change the access of the contributor to "Owner" using [this guide](https://help.github.com/en/github/setting-up-and-managing-organizations-and-teams/changing-a-persons-role-to-owner)
**Only trusted PERL members should be given "Owner" status**

NOTE: The Oxford-PERL organisation has been set up with [OAuth app restrictions removed](https://help.github.com/en/github/setting-up-and-managing-organizations-and-teams/disabling-oauth-app-access-restrictions-for-your-organization), such that members  can use third party applications including command line or Fork to make changes to the repository.

## Cloning the repository
Now you've been added to the PERL Repository on GitHub you need to clone it to a location on your PC (e.g. the desktop). In order to do this, it's best for you to have a 'git client' installed. There are quite a few available but any of the following would suffice: Fork, GitHub Desktop, GitKraken, GitGui. 

Once you have one of the above installed go to: (https://github.com/Oxford-PERL/ETB-analysis) and click the "Clone or download" button and copy the link it provides.

In your git client, navigate to the "Clone" function (e.g. in Fork: File --> Clone... ) and paste the link into the "Repository URL" section then select a "Parent Directory" (this is where the GitHub repository will live on your PC). This can be on your desktop or in a folder, whichever you prefer.

Finish by pressing the "Clone" button. In the Parent Directory you will now have an exacy copy of the PERL/ETB-Analysis repository that is on GitHub!


## Making a change (committing to a repo)
When editing any file in the cloned repository (whether you're using a Git client or on the GitHub website), the changes you make are being tracked. 

For example, you can add your name to the list of contributors in the README.md on the GitHub website. 

On the "Code" tab of the ETB-Analysis repository the file README.md can be edited clicking the pencil on the right side of the page. Now you can add your name under the "## Contributors" subheading. 

Once you've typed it in you can scroll to the bottom of that page where there is a box called "Commit changes". For your name to be added to the contributors on README.md you need to commit the change. When you commit changes, GitHub requires you to give a title to your commit which should outline what you've done (e.g. Updated README.md). When making big changes to a file/s it is good practice to provide a more detailed description of what you've changed too.

NOTE That adding your name but not committing the change is like editing a word document but not saving it afterwards. On GitHub "saving" is "committing", any changes you commit to any file will update that file on the branch you're working from. To start with, we will all be working from the "master" branch, committing changes to this branch will mean that file is changed for everyone working from that branch when they pull from the repository (more on that below).

NOTE When working from a cloned repository on your PC (as described above) there is an extra step to this process called "pushing" (see below)

## Add, commit, push, pull
### Add
You can easily add files to the repository via the GitHub website by clicking "Upload files" on the "Code" tab of the repository. Drag and drop or find the files you want to upload (e.g. a new ECAT analysis script you're working on) and commit the changes.

### Push
When working from a cloned repo (i.e. on your PC not on the GitHub website directly) you also need to push any changes you commit in order for the branch to be updated. To begin with, we will all likely be working from the "master" branch. When you make changes on this branch via a cloned repo the files will you've changed will only update on the branch (and so, for everyone else working from them) when you push your changes to the branch. Here's an example when working from Fork (all Git clients follow similar steps):

When you make a change to a file on the cloned repository, it will appear in the "Changes" (on left on Fork interface). Click on "Changes" and you will see all the "Unstaged" changes you've made to files in the repository. You may have made changes to multiple files but you may only want to commit and push some of them. On the "Changes" tab, you can select  the changes you want to commit and "Stage" them by clicking the "Stage" button.

Staged changes will now appear in the bottom section. To commit these changes you must add a "Commit subject" and a description of the changes (optional) and click "Commit (1) file". File changes have now been "saved".

To update the files on the main repository these changes now need to be pushed to the "master" branch. On Fork, you do this simply by clicking the arrow in the top bar pointing upwards. Now the latest version of the files on the repository will include your changes.

When working collaboratively, pushing changes you make and describing them fully is important. It's good practice to push any changes you make every time you finish working on something.

### Pull
In order to get the latest versions of all the files on the repository you need to "pull them down" from the respository. On Fork, you do this by clicking the arrow pointing downwards (in the middle of the the three, not the hollowed out one). You now have fully up to date versions of all the files.

When multiple collaborators are working on the same files and/or the same branch, pulling the latest file versions down from the repository is important and should be done before you start working on the files yourself. If you know others are actively working on these files, you should do this everytime you work on the files.
